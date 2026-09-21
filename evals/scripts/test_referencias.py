# -*- coding: utf-8 -*-
"""Que las rutas que los documentos citan existan de verdad.

**382 referencias cruzadas y nadie las habia comprobado nunca.** Cinco estaban
rotas, y del peor tipo posible: apuntaban a `evals/<fixture>.md` cuando el
fixture vive en `docs/skills-support/evals/`. **`evals/` existe** -- es el banco
de medicion -- asi que un lector iria a mirar ahi, no lo encontraria, y
concluiria que el fixture no existe. Una de ellas estaba en una INSTRUCCION de
un ADR Accepted: *«comprobar contra evals/adversarial-benchmark.md»*.

Es la misma decadencia silenciosa que el ESTADO-DEL-PROYECTO: nada avisa. Un
enlace roto no se ve al leer -- se ve al seguirlo, y nadie los sigue todos.

**Lo que NO cuenta como rota, y cada exclusion tiene su razon:**

  * Patrones y marcadores: `skills/*/SKILL.md`, `SPEC-NN`, `<nombre>`, `…`.
    No son rutas, son plantillas.
  * Rutas de OTROS repositorios. `docs/compilation.md` es de `better-sqlite3`
    y el propio documento lo dice con su URL completa dos lineas mas abajo.
    **Este fue el primer falso positivo de esta prueba**, y la exclusion se
    escribe con la lista de duenos ajenos, no con una excepcion por archivo.
  * `plugins/despacho/skills/fact-builder/`, que se borro el 2026-08-26.
    **Las 55 menciones se dejan a proposito**: son registro historico, y
    reescribirlas falsearia lo que se decidio entonces (BACKLOG §12).
  * `memory/…`, que es la carpeta que el asistente guarda por maquina y
    **no puede estar versionada** (registrado en el PASE-REAL).

    python3 evals/scripts/test_referencias.py
"""
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]

REF = re.compile(r"`((?:docs|plugins|evals|experiments|memory)/[^`\s]+?)`")

# Rutas que pertenecen a OTROS repositorios y aparecen citadas como tales.
AJENAS = {
    "docs/compilation.md",          # WiseLibs/better-sqlite3
}

# Lo que se dejo roto a proposito, con donde esta escrito por que.
DELIBERADAS = {
    "plugins/despacho/skills/fact-builder/",   # BACKLOG §12: registro historico
    "memory/contexto-b-inspeccion-salento.md",  # no versionable; ver PASE-REAL
}


def es_patron(ruta):
    return ("*" in ruta or "…" in ruta or "<" in ruta
            or "NNN" in ruta or re.search(r"SPEC-NN\b", ruta))


def rotas():
    fuera = {}
    for f in sorted(RAIZ.rglob("*.md")):
        if ".git" in f.parts:
            continue
        for m in REF.finditer(f.read_text(encoding="utf-8", errors="replace")):
            ruta = m.group(1).rstrip(".,;:)")
            if es_patron(ruta) or ruta in AJENAS or ruta in DELIBERADAS:
                continue
            base = ruta.split(":")[0]          # admite `archivo.md:100`
            if not (RAIZ / base).exists():
                fuera.setdefault(base, set()).add(str(f.relative_to(RAIZ)))
    return fuera


class LasRutasCitadasExisten(unittest.TestCase):

    def test_ninguna_referencia_apunta_al_vacio(self):
        r = rotas()
        self.assertEqual({}, r, "\n".join(
            "%s  <- citada en %s" % (k, ", ".join(sorted(v)))
            for k, v in sorted(r.items())))

    def test_la_prueba_mira_algo(self):
        """Control positivo: si el patron dejara de casar, pasaria sola."""
        total = 0
        for f in RAIZ.rglob("*.md"):
            if ".git" not in f.parts:
                total += len(REF.findall(f.read_text(encoding="utf-8",
                                                     errors="replace")))
        self.assertGreater(total, 300, "solo %d referencias: el patron se rompio"
                           % total)


class LoQueSeDejoRotoAProposito(unittest.TestCase):
    """Cada exclusion tiene que seguir siendo cierta, o deja de ser exclusion."""

    def test_fact_builder_sigue_sin_existir(self):
        """Si alguien lo recrea, la exclusion sobra y hay que quitarla."""
        self.assertFalse((RAIZ / "plugins/despacho/skills/fact-builder").exists())

    def test_y_su_sucesor_si_existe(self):
        self.assertTrue((RAIZ / "plugins/despacho/skills/hechos-con-prueba").exists())

    def test_la_ruta_ajena_se_declara_como_ajena(self):
        """`docs/compilation.md` tiene que seguir viniendo con su URL al lado.

        Sin esa URL, la exclusion seria una excepcion a dedo. Con ella, es un
        hecho comprobable del documento.
        """
        t = (RAIZ / "docs/research/runtime-dependencies-spike-v0.md").read_text(
            encoding="utf-8")
        self.assertIn("better-sqlite3/blob/master/docs/compilation.md", t)

    def test_el_memory_dangling_viene_con_su_explicacion(self):
        t = (RAIZ / "docs/PASE-REAL-SALENTO-2026-08-27.md").read_text(
            encoding="utf-8")
        self.assertIn(u"no está en el repositorio ni puede estarlo", t)


if __name__ == "__main__":
    unittest.main(verbosity=2)
