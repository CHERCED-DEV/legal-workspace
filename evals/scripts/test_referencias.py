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


class LosIDENTIFICADORESCitadosExisten(unittest.TestCase):
    """SPEC-NN, ADR-NNN y §N del backlog, contados contra los que hay.

    Son 192 referencias a specs, 2.755 a ADR, 69 internas dentro de los propios
    `SKILL.md` y 15 a secciones del backlog. **Ninguna se habia comprobado.**

    Las internas de los `SKILL.md` son las que mas importan aunque hoy esten
    todas bien: **las lee el modelo**, y una que quede colgando por una
    renumeracion no falla, no avisa y no se ve -- degrada el metodo en silencio.
    """

    def _ids(self, carpeta, patron_archivo, grupo):
        return {p.name.split("-")[grupo] for p in (RAIZ / carpeta).glob(patron_archivo)}

    def test_las_spec_citadas_existen_o_se_citan_como_retiradas(self):
        """SPEC-02 y SPEC-07 se retiraron, y las tres citas lo dicen.

        Una spec retirada se sigue citando -- es historia -- pero **la cita
        tiene que decir que se retiro**, o el lector la busca y no la halla.
        """
        hay = self._ids("docs/specs", "SPEC-*.md", 1)
        retiradas = {"02", "07"}
        faltan = {}
        for f in sorted(RAIZ.rglob("*.md")):
            if ".git" in f.parts:
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"\bSPEC-(\d{2})\b", t):
                nn = m.group(1)
                if nn in hay:
                    continue
                if nn in retiradas:
                    # La cita tiene que explicarse en el mismo archivo.
                    explicada = re.search(r"(?i)retirad|no hace falta|ya estaba", t)
                    self.assertTrue(explicada,
                                    "%s cita SPEC-%s sin decir que se retiro"
                                    % (f.relative_to(RAIZ), nn))
                    continue
                faltan.setdefault(str(f.relative_to(RAIZ)), set()).add(nn)
        self.assertEqual({}, faltan)

    def test_todos_los_adr_citados_existen(self):
        hay = self._ids("docs/architecture/adrs", "ADR-*.md", 1)
        faltan = {}
        for f in sorted(RAIZ.rglob("*.md")):
            if ".git" in f.parts:
                continue
            for m in re.finditer(r"\bADR-(\d{3})\b",
                                 f.read_text(encoding="utf-8", errors="replace")):
                if m.group(1) not in hay:
                    faltan.setdefault(str(f.relative_to(RAIZ)), set()).add(m.group(1))
        self.assertEqual({}, faltan)

    def test_las_secciones_del_backlog_citadas_existen(self):
        bl = (RAIZ / "docs/BACKLOG-CONSOLIDADO.md").read_text(encoding="utf-8")
        secciones = set(re.findall(r"(?m)^##\s+§(\d+(?:\.\d+)?)", bl))
        self.assertGreater(len(secciones), 10)
        faltan = {}
        for f in sorted(RAIZ.rglob("*.md")):
            if ".git" in f.parts:
                continue
            t = f.read_text(encoding="utf-8", errors="replace")
            for m in re.finditer(r"(?:BACKLOG|backlog)[^.\n]{0,30}?§\s?(\d+(?:\.\d+)?)", t):
                s = m.group(1)
                if s not in secciones and s.split(".")[0] not in secciones:
                    faltan.setdefault(str(f.relative_to(RAIZ)), set()).add(s)
        self.assertEqual({}, faltan)

    def test_las_referencias_internas_de_los_skill_resuelven(self):
        """Las 69 que lee el modelo. Una colgando degrada el metodo en silencio."""
        faltan = {}
        for f in sorted((RAIZ / "plugins/despacho/skills").glob("*/SKILL.md")):
            t = f.read_text(encoding="utf-8")
            hay = set(re.findall(r"(?m)^#{2,4}\s+(\d+(?:\.\d+)*)\.?\s", t))
            for c in set(re.findall(r"§\s?(\d+(?:\.\d+)*)", t)):
                if c not in hay and c.split(".")[0] not in hay:
                    faltan.setdefault(f.parent.name, set()).add(c)
        self.assertEqual({}, faltan)


class ElCorteDelBacklogCubreTodosLosADR(unittest.TestCase):
    """§7.1 parte los ADR en «gobiernan lo construido» y «no». Falta uno y se cree.

    El corte se hizo el 2026-09-05 sobre dieciocho ADR, **por rangos**: «001 a
    011», «012 a 018». Un rango envejece de la peor manera que hay: sigue
    leyendose bien cuando ya no cubre todo. El 2026-09-22 llegaron cuatro ADR
    mas y el corte siguio diciendo dieciocho **sin que nada fallara**.

    Esta prueba lee los rangos del propio §7 y comprueba que entre todos cubran
    cada ADR del disco. Si aparece un ADR-023 y nadie lo clasifica, falla.
    """

    ADRS = RAIZ / "docs" / "architecture" / "adrs"
    BACKLOG = RAIZ / "docs" / "BACKLOG-CONSOLIDADO.md"

    def _numeros_en_disco(self):
        return sorted(int(p.name[4:7]) for p in self.ADRS.glob("ADR-*.md"))

    def _cubiertos_por_el_corte(self):
        """Los rangos «| **001 a 011** |» de la tabla de §7.1, expandidos."""
        t = self.BACKLOG.read_text(encoding="utf-8")
        i = t.index(u"### 7.1 El corte")
        j = t.index(u"### 7.2", i)
        cubiertos = set()
        for a, b in re.findall(r"\|\s*\*\*(\d{3}) a (\d{3})\*\*\s*\|", t[i:j]):
            cubiertos |= set(range(int(a), int(b) + 1))
        return cubiertos

    def test_el_corte_cubre_todos_los_adr_del_disco(self):
        cubiertos = self._cubiertos_por_el_corte()
        sin_clasificar = [n for n in self._numeros_en_disco() if n not in cubiertos]
        self.assertEqual([], sin_clasificar,
                         u"§7.1 no dice si estos ADR gobiernan lo construido: %s"
                         % sin_clasificar)

    def test_el_corte_no_clasifica_lo_que_no_existe(self):
        """La mitad que se olvida: un rango que sigue nombrando un ADR retirado."""
        en_disco = set(self._numeros_en_disco())
        sobran = sorted(n for n in self._cubiertos_por_el_corte() if n not in en_disco)
        self.assertEqual([], sobran, u"§7.1 clasifica ADR que no están en el disco")

    def test_los_rangos_se_leyeron_de_verdad(self):
        """Control positivo: un patron que no casara con nada pasaria solo."""
        self.assertGreater(len(self._cubiertos_por_el_corte()), 15)

    def test_el_titulo_del_7_dice_cuantos_hay(self):
        """Y que el numero escrito sea el del disco, no el de septiembre."""
        t = self.BACKLOG.read_text(encoding="utf-8")
        self.assertEqual(23, len(self._numeros_en_disco()),
                         u"cambió el número de ADR: actualice el título de §7")
        self.assertIn(u"dieciocho entonces, veintitrés hoy", t)

if __name__ == "__main__":
    unittest.main(verbosity=2)
